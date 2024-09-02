from typing import Optional, Union

from dialogicai.utils import current_time, generate_uuid


class Metadata:
    def __init__(self, message_id=None, branches=None, created_at=None, parent_id=None):
        self.message_id = message_id if message_id else generate_uuid()
        self.branches = branches if branches else ["main"]
        self.created_at = created_at if created_at else current_time()
        self.parent_id = parent_id
    
    def to_dict(self):
        return {
            "message_id": self.message_id,
            "branches": self.branches,
            "created_at": self.created_at,
            "parent_id": self.parent_id
        }
    
    def __str__(self):
        return str(self.to_dict())



class NodeMessage:
    def __init__(self, content, role, metadata: Optional[Union[Metadata, dict]] = None):
        if isinstance(metadata, dict):
            metadata = Metadata(**metadata)
        self.content = content
        self.role = role
        self.metadata = metadata if metadata else Metadata()
    
    def to_dict(self):
        return {
            "content": self.content,
            "role": self.role,
            "metadata": self.metadata.to_dict()
        }


class DialogicAI:
    def __init__(self):
        self.thread: list = []
        self.branch_ref: dict = {
            "main": {
                "last_message": None,
                "length": 0
            }
        }
        self.target_branch = "main"
        self.before_branch = None
    
    # Setter and getter
    def set_last_message_by_branch(self, branch=None, message_id=None):
        """
        Set the last message ID in a branch.
        """
        branch = branch if branch else self.target_branch
        self.branch_ref[branch]["last_message"] = message_id
        self.branch_ref[branch]["length"] = self.branch_ref[branch]["length"] + 1 if self.branch_ref[branch]["length"] else 1
    

    def set_target_branch(self, branch):
        """
        Set the target branch.
        """
        self.before_branch = self.target_branch
        self.target_branch = branch
    

    def get_parent(self, branch=None):
        """
        Get the parent ID of the last message in the current branch.

        Args:
            branch (str): The branch to get the parent ID from.

        Returns:
            str: The parent ID of the last message in the current branch.
        """
        branch = branch if branch else self.target_branch
        if branch not in self.branch_ref:
            raise KeyError(f"Branch '{branch}' not found.")
        if self.branch_ref[branch]["length"] == 0 and branch == "main":
            return None
        if self.branch_ref[branch]["length"] == 0 and branch != "main":
            branch = self.before_branch
        if self.branch_ref[branch]["last_message"] is None:
            return None
        return self.branch_ref[branch]["last_message"]


    def get_message(self, message_id):
        """
        Get a message by its ID.

        Args:
            message_id (str): The ID of the message to retrieve.

        Returns:
            NodeMessage: The message with the specified ID.
        """
        for message in self.thread:
            if message.message_id == message_id:
                return message
        return None
    
    def get_last_message(self):
        """
        Get the last message in the current branch.

        Returns:
            NodeMessage: The last message in the current branch.
        """
        return self.get_message(self.get_parent())
    

    def update_branches_in_message(self, message_id, branch):
        """
        Update the branches of a message.

        Args:
            message_id (str): The ID of the message to update.
            branch (str): The branch to add.

        Returns:
            list: The updated list of branches.
        """
        if not branch or not message_id:
            return
        for message in self.thread:
            if message.metadata.message_id == message_id:
                if branch not in message.metadata.branches:
                    message.metadata.branches.append(branch)
                break
        return message.metadata.branches



    # Methods
    def change_branch(self, branch):
        """
        Change the current branch.

        Args:
            branch (str): The name of the new branch.
            
        Returns:
            str: The name of the new branch.
        """
        if branch not in self.branch_ref:
            self.branch_ref[branch] = {
                "last_message": None,
                "length": 0
            }
        self.set_target_branch(branch)
        return self.target_branch


    def add_message(self, message: Optional[Union[NodeMessage, dict]] = None):
        """
        Add a message to the thread.

        Args:
            message (NodeMessage or dict): The message to add.
        
        Returns:
            NodeMessage: The added message.
        """
        if not message:
            return
        if isinstance(message, NodeMessage):
            message = message.to_dict()
        
        if isinstance(message, dict):
            if "content" not in message or "role" not in message:
                raise ValueError("Invalid message format")

            # Define branch
            branch = message.get("metadata", {}).get("branches", [self.target_branch])[0]
            if branch != self.target_branch:
                branch = self.change_branch(branch)
            
            # Get parent ID
            parent_id = message.get("metadata", {}).get("parent_id")
            if not parent_id:
                parent_id = self.get_parent(branch)
            
            # Reference branch in parent message node
            if parent_id:
                self.update_branches_in_message(parent_id, branch)

            message_dict = {
                "content": message["content"],
                "role": message["role"],
                "metadata": {
                    "message_id": message.get("message_id"),
                    "branches": message.get("branches", [branch]),
                    "created_at": message.get("created_at"),
                    "parent_id": parent_id
                }
            }
            message = NodeMessage(**message_dict)

        self.thread.append(message)
        self.set_last_message_by_branch(branch, message.metadata.message_id)

        return message.to_dict()


    def thread_to_list(self):
        """
        Convert the thread to a list of dictionaries.

        Returns:
            list: A list of dictionaries representing the thread.
        """
        def convert_to_dict(obj):
            if isinstance(obj, NodeMessage):
                return obj.to_dict()
            elif isinstance(obj, Metadata):
                return obj.to_dict()
            elif isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            return obj
            

        return [convert_to_dict(message) for message in self.thread]