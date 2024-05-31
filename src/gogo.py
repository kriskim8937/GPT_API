from gpt_4 import get_gpt4_response
from dall_e_3 import get_dall_e_3_response
from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
)


def translate_and_summarize(news):
    prompt = "Translate to English and summrize to 5 sentences:\n\n" + news.content
    return get_gpt4_response(prompt)


def get_revised_prompt(prompt):
    prompt = "Remove sensitive words from below sentence:\n\n" + prompt
    return get_gpt4_response(prompt)


def main():
    # news_list = get_news()
    # updated_news = translate_and_summarize(news_list[0])
    # print(updated_news)
    # generate_audio(updated_news)
    script = """
    A physical education teacher has been sentenced to three and a half years in prison for secretly filming over 100 elementary school girls at a prestigious school in central Sweden. Both the prosecutors and the man's lawyer have appealed the verdict, with the prosecution seeking a longer sentence. The offenses were discovered two years ago when colleagues caught the man filming girls changing during a school trip, leading to a police raid where vast amounts of child exploitation material were found. Despite a history of complaints and inappropriate behavior dating back over 20 years, the teacher managed to remain employed at various schools. Now, both the prosecutor and a parent of one of the victims believe only the maximum penalty is appropriate given the severity and 
    number of the incidents.
    """
    create_video_from_text(script)
    # prompts = """
    # A physical education teacher was sentenced to three and a half years in prison for secretly filming over 100 young girls at a prestigious school in Central Sweden.
    # """.split(". ")
    # for prompt in prompts:
    #     print(prompt)
    #     new_func(prompt)


def create_image(prompt):
    result = get_dall_e_3_response(prompt)
    while not result:
        prompt = get_revised_prompt(prompt)
        print(prompt)
        result = get_dall_e_3_response(prompt)
    return result


def create_video_from_text(text):
    # Create audio
    audio_clip = AudioFileClip(r"outputs\audios\audio_2024-05-31-17-29-01.mp3")

    # Split text for each image (assuming each image holds one sentence for simplicity)
    sentences = text.split(". ")
    image_files = []
    clips = []

    for i, sentence in enumerate(sentences):
        image_path = create_image(sentence)
        print(image_path)
        image_files.append(image_path)

        image_clip = ImageClip(image_path).set_duration(
            audio_clip.duration / len(sentences)
        )
        clips.append(image_clip)

    # Concatenate all image clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Combine audio and video
    final_video = final_clip.set_audio(audio_clip)

    # Write the final video file
    final_video.write_videofile("output_video.mp4", fps=24)


if __name__ == "__main__":
    main()
