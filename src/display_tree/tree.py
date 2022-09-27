from typing import Any, List, Optional, Set, Tuple

debug_val = 0

class Tree:
    # Minimalistic Constructor
    def __init__(
            self,
            value: Any,
            parent: Optional["Tree"] = None,
            children: List["Tree"] = [],
            padding: int = 1,
            branches: Tuple[str, str, str] = ('/', '|', '\\')
        ):
        # Display Properties
        self.value = value
        self.padding: int = padding
        self.branches: Tuple[str, str, str] = branches

        # Tree Properties
        if parent is not None:
            self.parent: Optional["Tree"] = parent
            self.parent.children.append(self)
        else:
            # Root node
            self.parent: Optional["Tree"] = None

        if len(children) > 0:
            self.children: List["Tree"] = children
            for child in self.children:
                child.parent = self
        else:
            self.children: List["Tree"] = []

        # Hidden Properties
        self._height: int = 1
        self._width: int = 0
        self._sub_width: int = 0
        self._pad_left: int = 0
        self._pad_right: int = 0
        self._bal_coef: int = 0

    def __str__(self):
        return self.display()

    def isLeaf(self):
        return len(self.children) == 0

    def _update_upward(self):
        if self.isLeaf():
            self._height = 1
            self._width = len(str(self.value))
            self._sub_width = self._width
        else:
            sub_height: int = 0
            sub_width: int = 0
            for child in self.children:
                child._update_upward()
                sub_height = max(sub_height, child._height)
                sub_width += (child._width + self.padding)

            self._height = sub_height + 1
            self._sub_width = sub_width - self.padding
            self._width = max(self._sub_width, len(str(self.value)))

    def _update_downward(self):
        if self._width > self._sub_width:
            extra_padding = self._width - self._sub_width
            left_padding = extra_padding // 2
            right_padding = extra_padding - left_padding

            self._pad_left = left_padding
            self._pad_right = right_padding

        # Update child nodes recursively
        for child in self.children:
            child._update_downward()

    def _update_dimensions(self):
        self._update_upward()
        self._update_downward()

    @staticmethod
    def _padding_block(height: int, width: int):
        return [' ' * width] * height

    def _default_padding_block(self):
        return self._padding_block(height=2 * (self._height - 1), width=self.padding)

    @staticmethod
    def _expand_block(block: List[str], height: int = 0, width: int = 0) -> List[str]:
        target_height: int = len(block) if height == 0 else height
        target_width: int = len(block[0]) if width == 0 else width
        expanded_block: List[str] = []
        for i in range(target_height):
            if i < len(block):
                expanded_block.append(f"{block[i]:<{target_width}}")
            else:
                expanded_block.append(' ' * target_width)
        return expanded_block

    @staticmethod
    def _pad_branch(branch: str, width: int, bal_coef: int):
        return ' ' * abs(bal_coef) + f"{branch:^{width}}"

    @staticmethod
    def _hstack_blocks(blocks: List[List[str]]):
        stacked_block: List[str] = []
        for layer in zip(*blocks):
            stacked_block.append(''.join(layer))
        return stacked_block

    @staticmethod
    def _vstack_blocks(blocks: List[List[str]]):
        stacked_block: List[str] = []
        for block in blocks:
            for layer in block:
                stacked_block.append(layer)
        return stacked_block

    def symbol(self):
        return str(self.value)

    def _block(self) -> List[str]:
        if self.isLeaf():
            # Leaf node
            return [' ' * self._pad_left + self.symbol() + ' ' * self._pad_right]
        else:
            # Internal node

            # Current block header
            block_head = [f"{self.symbol():^{self._width}}"]

            # Child Blocks
            child_blocks: List[List[str]] = []
            for i, child in enumerate(self.children):
                global debug_val
                debug_val += 1
                # Determine branch type
                if len(self.children) == 1:
                    branch = self.branches[1]
                elif i == 0:
                    branch = self.branches[0]
                elif i == len(self.children) - 1:
                    branch = self.branches[-1]
                else:
                    branch = self.branches[1]

                # Generate child block recursively
                child_block = child._block()
                child_branch = self._pad_branch(branch=branch, width=child._width, bal_coef=child._bal_coef)
                child_block.insert(0, child_branch)
                child_block = self._expand_block(block=child_block, height=2 * (self._height - 1))

                # If not first block, append padding block first
                if i > 0:
                    child_blocks.append(self._default_padding_block())

                # Append the child block
                child_blocks.append(child_block)

            # Padding blocks
            left_padding_block = self._padding_block(height=2 * (self._height - 1), width=self._pad_left)
            right_padding_block = self._padding_block(height=2 * (self._height - 1), width=self._pad_right)

            # Concatenate the blocks
            block_body: List[str] = self._hstack_blocks(blocks=[left_padding_block, *child_blocks, right_padding_block])
            # block_body: List[str] = self._hstack_blocks(blocks=child_blocks)
            complete_block: List[str] = self._vstack_blocks(blocks=[block_head, block_body])

            return complete_block

    @staticmethod
    def _resolve_block(block: List[str]) -> str:
        return '\n'.join(block)

    def display(self) -> str:
        '''
        Concatenates tree blocks to produce
        '''

        # Update tree dimensions
        self._update_dimensions()

        # Build blocks recursively
        block: List[str] = self._block()

        return self._resolve_block(block=block)

    @staticmethod
    def _verify_block(block: List[str]):
        if len(block) > 0:
            width: int = len(block[0])
            for layer in block:
                if len(layer) != width:
                    raise ValueError("Invalid block")

    def debug(self, depth: int = 0, props: Tuple = ("v", "h", "w", "_w", "bc", "pl", "pr")):
        if depth == 0:
            self._update_dimensions()
        definitions = {
            "v": self.value,
            "p": self.padding,
            "b": self.branches,
            "h": self._height,
            "w": self._width,
            "_w": self._sub_width,
            "bc": self._bal_coef,
            "pl": self._pad_left,
            "pr": self._pad_right,
        }
        info = "; ".join(map(lambda x: f"{x}:{definitions.get(x)}", props))
        print("  " * (depth - 1) + ("L " if depth >= 1 else "") + info)
        for child in self.children:
            child.debug(depth=depth + 1)
