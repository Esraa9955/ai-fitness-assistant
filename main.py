from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
load_dotenv()
client = OpenAI()
model='gpt-3.5-turbo-16k'
# create our assistant 
# personal_trainer_asses = client.beta.assistants.create(
# name="Personal Trainer",
# instructions="""you are the best personal trainer and nutritionist who knows how to get client to build learn muscles. you have trained high-caliber athletes and movie stares. """,
# model=model,
# )

# assistant_id=personal_trainer_asses.id
# print(assistant_id)



# thread = client.beta.threads.create(
#   messages=[
#     {
#       "role":"user",
#       "content":"How do I get started working out to lose fat and build muscle?",
#     }
#   ]
# )

# thread_id=thread.id
# print(thread_id)


# hardcode our ids 
assistanat_id= "asst_RTdduyuVZ7sRkQpCJ6wsgqOq"
thread_id= "thread_AhPLimxfW6z3nYpMpDxMWJqn"
# create a Message
# message = "what are the best exercises for lean muscles and getting strong "
message = "How much water should i drink in a day to get healthy "
message = client.beta.threads.messages.create(
  thread_id= thread_id,
  role= "user",
  content=message

)

# Run our assistant
run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistanat_id,
  instructions= "Please address the user as James Bond "
)

def wait_for_run_completion(client,thread_id,run_id,sleap_interval=5):
  """whats for a run complete and prints the elapsed time. :param client: the OpentAI client object.
  :param thread_id: the ID of the thread.
  :param run_id: The ID of the run.
  :param sleep_interval:Time in seconds to wait between checks."""
  while True:
    try:
      run = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run_id)
      if run.completed_at:
        elapsed_time =run.completed_at - run.created_at
        formatted_elapsed_time = time.strftime(
          "%H:%M:%S", time.gmtime(elapsed_time)
        )
        print(f"Run completed in {formatted_elapsed_time}")
        logging.info(f"Run completed in {formatted_elapsed_time}")
        # Get messages here once Run is completed!
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        print(f"Assistant Response:{response}")
        break
    except Exception as e:
      logging.error(f"An error occurred while retrieving the run: {e}")
      break
    logging.info("waiting for run to complete...")
    time.sleep(sleap_interval)



# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Steps---> {run_steps.data[0]}")