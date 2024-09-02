# 🎉 DialogicAI

**DialogicAI** is a Python package designed to manage complex, threaded conversations with branching capabilities, much like version control systems manage code branches. Whether you're building an AI chatbot, a customer support system, or any application that requires structured conversations, DialogicAI provides the tools to seamlessly manage multiple conversation threads, switch between branches, and keep track of message history.

## 🚀 Installation

You can install DialogicAI directly from PyPI using pip:

```bash
pip install dialogicai
```

## 🏃‍♂️ Quick Start

Here’s a quick example to get you started with DialogicAI:

```python
from dialogicai import DialogicAI

# Initialize the DialogicAI instance
dialogicAI = DialogicAI()

# Add some messages
dialogicAI.add_message({"content": "Hello, how are you?", "role": "user"})
dialogicAI.add_message({"content": "I'm doing well, thank you! How can I assist you today?", "role": "assistant"})

# Branch the conversation
dialogicAI.add_message({
    "content": "Can you tell me a joke?", 
    "role": "user",
    "metadata": {"branches": ["joke"]}
})

# Convert the thread to a list of dictionaries
conversation = dialogicAI.thread_to_list()
print(conversation)
```


## 🛠️ Main Methods

DialogicAI provides a set of powerful methods to help you manage conversation threads with ease. Here are some of the key methods:

### ➕ `add_message(message)`
This method adds a new message to the current conversation thread.

- **Parameters**: 
  - **message** (dict): A dictionary containing the message's `content`, `role`, and optional `metadata` (such as branches).
  
- **Usage Example**:
  ```python
  dialogicAI.add_message({"content": "Hello, how are you?", "role": "user"})
  ```


### 🔄 `change_branch(branch)`
Switches the current conversation to a different branch, allowing you to manage multiple threads seamlessly.

- **Parameters**:
  - **branch** (str): The name of the branch you wish to switch to.
  
- **Usage Example**:
  ```python
  dialogicAI.change_branch("joke")
  ```


### 📩 `get_last_message()`
Retrieves the last message in the current branch, making it easy to continue a conversation or review the last interaction.

- **Returns**:
  - **NodeMessage**: The last message object in the current branch.
  
- **Usage Example**:
  ```python
  last_message = dialogicAI.get_last_message()
  print(last_message.content)
  ```

### 📝 `thread_to_list()`
Converts the entire conversation thread into a list of dictionaries, making it straightforward to serialize or inspect the conversation history.

- **Returns**:
  - **list**: A list of dictionaries, each representing a message in the thread.
  
- **Usage Example**:
  ```python
  conversation_list = dialogicAI.thread_to_list()
  print(conversation_list)
  ```

## 🤝 Contributions

We welcome contributions from the community! If you have ideas for new features, find bugs, or want to enhance the code, feel free to get involved. Here’s how you can contribute:

1. 🍴 **Fork the repository**: Create your own copy of the project.
2. 🌿 **Create a new branch**: Use `git checkout -b feature-branch` to start working on a new feature or bug fix.
3. 💻 **Commit your changes**: Once your changes are ready, commit them with a meaningful message (`git commit -am 'Add new feature'`).
4. 📤 **Push to the branch**: Push your changes to your GitHub repository with `git push origin feature-branch`.
5. 🔄 **Open a Pull Request**: Submit your changes for review, and if approved, they’ll be merged into the project!

### 📐 Coding Standards
- We use **Black** for code formatting to ensure consistency across the codebase.
- All contributions should include relevant **pytest** tests to maintain code quality.

---

## 📬 Contact

I’m an AI Engineer with a passion for developing flawless products. Feel free to reach out if you have any questions, ideas, or just want to connect:

- **👤 Name**: Endy Bermudez Rodriguez  
- **📧 Email**: [endyb.dev@gmail.com](mailto:endyb.dev@gmail.com)  
- **🐙 GitHub**: [Check out my projects @endybits](https://github.com/endybits)  
- **💼 LinkedIn**: [Connect with me on LinkedIn](https://www.linkedin.com/in/endyb/)
