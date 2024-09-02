# tests/test_dialogicai.py
import pytest
from dialogicai.core import DialogicAI

def test_add_message_to_thread():
    dialogicAI: DialogicAI = DialogicAI()
    
    u1 = {"content": "Hello, how are you?", "role": "user"}
    dialogicAI.add_message(u1)

    assert len(dialogicAI.thread) == 1
    assert dialogicAI.thread[0].content == "Hello, how are you?"
    assert dialogicAI.thread[0].role == "user"
    assert dialogicAI.thread[0].metadata.branches == ["main"]

def test_add_message_with_new_branch():
    dialogicAI = DialogicAI()
    
    u1 = {"content": "Hello, how are you?", "role": "user"}
    dialogicAI.add_message(u1)
    
    u2 = {
        "content": "Can you tell me a joke?",
        "role": "user",
        "metadata": {"branches": ["joke"]}
    }
    dialogicAI.add_message(u2)
    
    assert len(dialogicAI.thread) == 2
    assert dialogicAI.thread[1].content == "Can you tell me a joke?"
    assert dialogicAI.thread[1].role == "user"
    assert dialogicAI.thread[1].metadata.branches == ["joke"]
    
    # Check that the first message has been updated with the new branch
    assert "joke" in dialogicAI.thread[0].metadata.branches

def test_thread_to_list():
    dialogicAI = DialogicAI()

    u1 = {"content": "Hello, how are you?", "role": "user"}
    a1 = {"content": "I'm doing well, thank you! How can I assist you today?", "role": "assistant"}
    
    dialogicAI.add_message(u1)
    dialogicAI.add_message(a1)

    thread_list = dialogicAI.thread_to_list()

    assert len(thread_list) == 2
    assert thread_list[0]["content"] == "Hello, how are you?"
    assert thread_list[1]["content"] == "I'm doing well, thank you! How can I assist you today?"
    
def test_change_branch_and_add_message():
    dialogicAI = DialogicAI()

    u1 = {"content": "Hello, how are you?", "role": "user"}
    dialogicAI.add_message(u1)
    
    u2 = {
        "content": "Can you tell me a joke?",
        "role": "user",
        "metadata": {"branches": ["joke"]}
    }
    dialogicAI.add_message(u2)
    
    # Change branch to "joke" and add a message
    dialogicAI.change_branch("joke")
    a2 = {"content": "Why don't scientists trust atoms? Because they make up everything!", "role": "assistant"}
    dialogicAI.add_message(a2)
    
    assert dialogicAI.target_branch == "joke"
    assert len(dialogicAI.thread) == 3
    assert dialogicAI.thread[2].content == "Why don't scientists trust atoms? Because they make up everything!"
    assert dialogicAI.thread[2].metadata.branches == ["joke"]

# def test_get_last_message():
#     dialogicAI = DialogicAI()

#     u1 = {"content": "Hello, how are you?", "role": "user"}
#     dialogicAI.add_message(u1)
    
#     u2 = {
#         "content": "Can you tell me a joke?",
#         "role": "user",
#         "metadata": {"branches": ["joke"]}
#     }
#     dialogicAI.add_message(u2)
    
#     last_message = dialogicAI.get_last_message()
    
#     assert last_message.content == "Can you tell me a joke?"
#     assert last_message.metadata.branches == ["joke"]