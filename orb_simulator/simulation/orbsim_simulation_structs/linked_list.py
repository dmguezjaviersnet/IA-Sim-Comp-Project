class LinkedListNode:

	def __init__(self, data):
		self.data = data
		self.next: LinkedListNode = None

class LinkedList:
    
	def __init__(self):
		self.head: LinkedListNode = None

	def insert(self, new_node):
		if self.head:
			last_node = self.head
			while last_node.next != None:
				last_node = last_node.next

			last_node.next = new_node

		else:
			self.head = new_node

	def remove(self, elem):
		if self.head:
			curr_item = self.head
			next_item = self.head.next

			if elem == curr_item.data:
				self.head = next_item

			else:
				while(next_item):
					if elem == next_item.data:
						curr_item.next = next_item.next
						break
					curr_item = next_item
					next_item = next_item.next

	def remove_at(self, index):
		if self.head:
			curr_item = self.head
			next_item = self.head.next
			next_item_index = 1

			if index == 0:
				self.head = next_item

			else:
				while(next_item_index < index):
					curr_item = next_item
					next_item = next_item.next
					next_item_index += 1
				
				curr_item.next = next_item.next