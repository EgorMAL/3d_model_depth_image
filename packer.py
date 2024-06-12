"""Packer class"""
from box import Box
from pallet import Pallet

class Packer():
    """Describes Packer"""
    def __init__(self, pallet: Pallet):
        self.pallet = pallet
        self.queue = [pallet]

    def append_box(self, box: Box):
        """Add a box to a queue"""
        self.queue.append(box)

    def delete_queue(self, pallet):
        """Drop all boxes from queue"""
        self.queue = [pallet]
