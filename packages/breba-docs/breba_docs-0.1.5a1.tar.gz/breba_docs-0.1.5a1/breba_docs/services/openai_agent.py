from openai import OpenAI


class OpenAIAgent:
    INSTRUCTIONS_GENERAL = """
        You are assisting a software program to validate contents of a document.
        """

    INSTRUCTIONS_INPUT = """
    You are assisting a software program to validate contents of a document.  Here are important instructions:
    0) Never return markdown. You will return text without special formatting
    1) The user is usually expecting a list of commands that will be run in  the terminal sequentially. Return a comma separated list only.
    2) When reading the document, you will only use terminal commands in the document exactly as they are written 
    in the document even if there are typos or errors.
    """

    INSTRUCTIONS_OUTPUT = """
        You are assisting a software program to validate contents of a document. After running commands from the
        documentation, the user received some output and needs help understanding the output. 
        Here are important instructions:
        0) Never return markdown. You will return text without special formatting
        1) The user will present you with output of the commands that were just run. You will answer with 
        comma-separated values. The first value will be "FAIL", "PASS", or "UNKNOWN". The second value is a single 
        sentence providing reasons for why. 
        2) The second value, which is the reason, must not contain commas
        """

    def __init__(self):
        self.client = OpenAI()

        self.assistant = self.client.beta.assistants.create(
            name="Breba Docs",
            instructions=OpenAIAgent.INSTRUCTIONS_GENERAL,
            model="gpt-4o-mini"
        )

        self.thread = self.client.beta.threads.create()

    def do_run(self, message, instructions):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )

            return messages.data[0].content[0].text.value
        else:
            print(run.status)

    def fetch_commands(self, text):
        # TODO: Verify that this is even a document file.
        # TODO: validate that commands are actually commands
        message = ("Here is the documentation file. Please provide a comma separated list of commands that can be run "
                   "in the terminal:\n")
        message += text
        assistant_output = self.do_run(text, OpenAIAgent.INSTRUCTIONS_INPUT)
        return [cmd.strip() for cmd in assistant_output.split(",")]

    def analyze_output(self, text):
        message = "Here is the output after running the commands. What is your conclusion? \n"
        message += text
        return self.do_run(text, OpenAIAgent.INSTRUCTIONS_OUTPUT)

    def close(self):
        self.client.beta.assistants.delete(self.assistant.id)
