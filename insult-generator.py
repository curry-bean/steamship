"""Insults you with AI

This project publishes an API & web demo to generate insults with GPT-3.

That's right. It's Insults as a Service (IaaS). 

Not the infrastructure you asked for, but the infrastructure you probably needed.

TO RUN:
1. Get a Steamship API Key (Visit: https://steamship.com/account/api).
2. Copy this key to a Replit Secret named STEAMSHIP_API_KEY.
3. Click the green `Run` button at the top of the window (or open a Shell and type `python3 api.py`).

To deploy it:
1. Close and re-open your console to make sure secrets are refreshed.
2. Run `ship deploy`

More information about this template is provided in README.md.

To learn more about advanced uses of Steamship, read our docs at: https://docs.steamship.com/packages/using.html.
"""
import inspect
from enum import Enum

from termcolor import colored

from steamship import check_environment, RuntimeEnvironments, Steamship
from steamship.invocable import post, PackageService

# This Enum causes will cause the auto-generated web UI to have a nice dropdown box
class InsultType(str, Enum):
  CLASSY = "1920s"
  SILLY = "Silly"
  DISMISSIVE = "Dismissive"
  SHAKESPEARE = "Shakespeare"
  PIRATE = "Pirate"


# Here are the prompts. They're surprisingly simple.
DISMISSIVE = "Please create a backhanded insult about {topic}. The insult should be subtle and dismissive."

CLASSY = 'Please create a classy 1920s style insult about {topic}. The insult feel like dated English from another time.'

SILLY = 'Please create a silly insult about {topic}. The insult should make a young child giggle and sound like a Dr. Seuss quote..'

SHAKESPEARE = 'Please create a Shakespeare insult about {topic}. The insult should sound as if it comes from a Shakespearean play.'

PIRATE = 'Arr Matey! Please create a pirate style insult about {topic}. The insult should sound as from the deck of a pirate ship.'

class PromptPackage(PackageService):
  """Generates insults of a selectable style."""

  @post("generate")
  def generate(self,
               topic: str = None,
               style: InsultType = InsultType.CLASSY) -> str:
    """Generate text from prompt parameters."""

    llm = self.client.use_plugin("gpt-3",
                                 config={
                                   "max_words": 100,
                                   "temperature": 0.8
                                 })

    if style == InsultType.CLASSY:
      prompt = CLASSY
    elif style == InsultType.SHAKESPEARE:
      prompt = SHAKESPEARE
    elif style == InsultType.SILLY:
      prompt = SILLY
    elif style == InsultType.DISMISSIVE:
      prompt = DISMISSIVE
    elif style == InsultType.PIRATE:
      prompt = PIRATE
    else:
      prompt = CLASSY

    return llm.generate(prompt, {"topic": topic})



# Try it out locally by running this file!
if __name__ == "__main__":
  print(colored("Generate Insults with GPT-3\n", attrs=['bold']))

  # This helper provides runtime API key prompting, etc.
  check_environment(RuntimeEnvironments.REPLIT)

  with Steamship.temporary_workspace() as client:
    package = PromptPackage(client)

    print(colored("Generating a few examples:", 'green'))

    valid = ['classy', 'shakespeare', 'pirate', 'dismissive', 'silly']
    
    examples = [
      ('this caviar', InsultType.CLASSY),
      ('your face', InsultType.SHAKESPEARE),
      ('this breakfast buffet', InsultType.PIRATE),
    ]

    for (topic, style) in examples:
      print(colored("Topic:", 'grey'), f"{topic}")
      print(colored("Style", 'grey'), f"{style}")
      print(colored("Generating...", 'grey'))
      print(colored("Insult:", 'grey'),
          f"{package.generate(topic=topic, style=style)}\n")

    print(colored("Now, try with your own inputs...", 'green'))

    try_again = True
    while try_again:
      print(colored(f"Valid styles are: {valid}", 'grey'))      
      kwargs = {}
      for parameter in inspect.signature(package.generate).parameters:
        kwargs[parameter] = input(
          colored(f'{parameter.capitalize()}: ', 'grey'))

      print(colored("Generating...", 'grey'))

      # This is the prompt-based generation call
      print(colored("Insult:", 'grey'), f'{package.generate(**kwargs)}\n')

      try_again = input(colored("Generate another (y/n)? ",
                                'green')).lower().strip() == 'y'
      print()

    print("Ready to share with your friends (and the world)?")
    print("Run ", colored("$ ship deploy ", color='green',
                          on_color='on_black'),
          "to get a production-ready API endpoint and web-based demo app.")
    print("That's right. It's Insults as a Service (IaaS).")