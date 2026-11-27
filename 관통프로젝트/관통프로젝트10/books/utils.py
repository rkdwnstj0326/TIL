import os
import uuid
from openai import OpenAI
from pathlib import Path
from django.conf import settings
from google import genai
import base64
from dotenv import load_dotenv


load_dotenv()

def generate_image_with_openai(thread_title, thread_content, book_title, book_author):

    keyword_extractor_prompt = (
        f"""
        {book_author}의 책 {book_title}을 읽고 쓴 독서 다이어리의 감정을 분석해 키워드 5개를 추출하시오.
        키워드 추출이 완료됐다면 키워드를 기반으로 이미지 생성 AI에 제공할 프롬프트를 작성하시오.
        해당 프롬프트를 통해 해당 독서 다이어리 페이지의 썸네일 이미지를 생성 예정.
        생성할 최종 이미지는 추상적이고 모호한 형태의 초현실주의적인 그림이어야 함. 

        <독서 다이어리>
            <제목>{thread_title}</제목>
            <본문>{thread_content}</본문>
        </독서 다이어리>

        <답변 예시>
            불안, 격정, 찬란함, 노스텔지아, 희망이 담긴 Abstract expressionism 스타일의 추상화
        </답변 예시>

        답변 : 
        """
    )
    api_key = os.getenv('GMS_KEY')
    base_url = os.getenv('GMS_URL')
    base_img_url = os.getenv('GMS_IMG_URL')
    if not all((api_key, base_url, base_img_url)):
        return None
    client = OpenAI(base_url=base_url, api_key=api_key)
    keyword_extractor_response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "당신은 이미지 생성 AI를 위한 프롬프트 작성 비서입니다."},
            {"role": "user", "content": keyword_extractor_prompt},
        ]
    )
    keyword_extractor_response = keyword_extractor_response.choices[0].message.content
    
    img_generator_prompt = keyword_extractor_response + " 어떠한 텍스트, 글자, 숫자, 심볼도 포함하지 않을 것"
    print(img_generator_prompt)

    img_client = genai.Client(
        api_key=api_key,
        http_options={"base_url": base_img_url}
    )
    response_img = img_client.interactions.create(
        model="gemini-3.1-flash-lite-image",
        input=img_generator_prompt,
    )

    # print(response_img.output_image)
    if response_img.output_image:
        output_dir = Path(settings.MEDIA_ROOT) / "thread_cover_img"
        output_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{uuid.uuid4()}.png"
        file_path = output_dir / file_name
        
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(response_img.output_image.data))
        return (Path("thread_cover_img") / file_name).as_posix()

    return None
