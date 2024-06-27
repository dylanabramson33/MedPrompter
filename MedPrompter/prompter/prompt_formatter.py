import anthropic

class PromptFormatter:
    def __init__(self, system_prompt, style_prompt_dict, task_prompt):
        self.system_prompt = system_prompt
        self.style_prompt_dict = style_prompt_dict
        self.task_prompt = task_prompt

    def format(self):
        output_prompt = ""
        for key, value in self.style_prompt_dict.items():
            output_prompt += f"{key}: {value}\n"

        output_prompt += f"\n {self.task_prompt}"
        return output_prompt


client = anthropic.Anthropic()
system_prompt = "You are a highly experienced physician tasked with documenting the details of a patient's hospital visit. You are thorough, professional, and health-focused. You care deeply about your patients' well-being and you want them to receive the best possible care. Your tone is report-like, clear, and detailed. Today you are tired, distracted, and prone to mishear your nurses, make mistakes and misunderstandings."
task_prompt = "In the same style and organization as the text above, write clinical notes for a patient who may have Fibrodysplasia Ossificans Progressiva without mentioning Fibrodysplasia Ossificans Progressiva directly. allow their symptoms to be very ambiguous but still somewhat indicative of the disease. you are tired and prone to some typos and errors and missing important information"

for i in range(10):
    transcription = df['transcription'][i]
    style_prompt_dict = transcription
    prompt_formatter = PromptFormatter(system_prompt, style_prompt_dict, task_prompt)
    prompt = prompt_formatter.format()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.2,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print(message.content)
