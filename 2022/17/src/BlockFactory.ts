import Tower from "./Tower.js";
import {
  Block,
  HorizontalBlock,
  PlusBlock,
  BackwardsLBlock,
  VerticalBlock,
  SquareBlock
} from "./blocks/index.js";

enum BlockType {
  HORIZONTAL = 0,
  PLUS = 1,
  BACKWARDSL = 2,
  VERTICAL = 3,
  SQUARE = 4
}

class BlockFactory {
  public static CreateBlock(blockType: number, tower: Tower): Block {
    switch (blockType) {
      case BlockType.HORIZONTAL:
        return new HorizontalBlock(tower);
      case BlockType.PLUS:
        return new PlusBlock(tower);
      case BlockType.BACKWARDSL:
        return new BackwardsLBlock(tower);
      case BlockType.VERTICAL:
        return new VerticalBlock(tower);
      case BlockType.SQUARE:
        return new SquareBlock(tower);
      default:
        alert("Error state!");
        return null;
    }
  }
}

export default BlockFactory;