import os
import subprocess
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Question


def build_docker_image(question):
    dockerfile_dir = os.path.join(
        settings.MEDIA_ROOT, 'dockerfiles', str(question.id))
    os.makedirs(dockerfile_dir, exist_ok=True)
    src_files_zip = f"http://192.168.1.31:3000{question.src_files_zip.url}"
    test_script = f"http://192.168.1.31:3000{question.test.url}"

    # Copy config and src_files_zip to the dockerfile_dir

    dockerfile_content = f"""
    FROM python
    # FROM python:3.8-slim

    WORKDIR /app

    RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

    # Download and extract the zip file
    ARG ZIP_URL={src_files_zip}
    RUN wget -O temp.zip $ZIP_URL && unzip temp.zip && rm temp.zip

    # Download the additional Python file
    ARG PYTHON_FILE_URL={test_script}
    RUN wget -O script.py $PYTHON_FILE_URL

    # If requirements.txt exists, install the requirements
    RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    COPY . /app

    CMD ["tail", "-f", "/dev/null"]

    """

    with open('dockerfiles/Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    with open('dockerfiles/Dockerfile', 'r') as f:
        question.config.save(f.name, f)

    image_name = f"question_{question.id}_image"
    subprocess.run(["docker", "build", "-t", image_name,
                   "dockerfiles"], check=True)

    return image_name


def run_solution_in_docker(image_name, solution_code):
    container_name = f"container_{uuid.uuid4()}"
    temp_solution_file = '/tmp/temp_solution.py'

    sol = "\n".join(solution_code)
    with open(temp_solution_file, 'w') as f:
        f.write(sol)

    try:
        subprocess.run(["docker", "run", "--name",
                       container_name, "-d", image_name], check=True)
        subprocess.run(["docker", "cp", temp_solution_file,
                       f"{container_name}:/app/temp.py"], check=True)

        result = subprocess.run(["docker", "exec", container_name,
                                "python", "script.py"], capture_output=True, text=True)
        print("output:", result.stdout)
        print("error:", result.stderr)
        return {
            "output": result.stdout,
            "error": result.stderr
        }
    finally:
        subprocess.run(["docker", "rm", "-f", container_name])


@api_view(['POST'])
def create_assignment(request):
    data = request.data
    files = request.FILES
    # config = files.get('config')
    test = files.get('test')
    print(test)
    src = files.get('src')
    title = data.get('title')
    body = data.get('body')
    description = data.get('description')
    difficulty = data.get('difficulty')
    question = Question.objects.create(
        title=title,
        body=body,
        # config=config,
        test=test,
        src_files_zip=src,
        description=description,
        difficulty=difficulty
    )
    try:
        image_name = build_docker_image(question)
        question.docker_image = image_name
        question.save()
        return Response({"message": "Assignment created successfully"}, status=status.HTTP_201_CREATED)
    except subprocess.CalledProcessError as e:
        question.delete()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def submit_solution(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

    solution_code = request.data.get('solution_code')
    if not solution_code:
        return Response({"error": "No solution code provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        output = run_solution_in_docker(
            question.docker_image, solution_code)
        return Response({"output": output}, status=status.HTTP_200_OK)
    except subprocess.CalledProcessError as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
