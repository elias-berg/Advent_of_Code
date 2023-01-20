import { Block } from "./Block.js";
import Tower from "../Tower.js";

export class VerticalBlock extends Block {
  constructor(tower: Tower) {
    super(tower);

    this.Height = 4;
    this.Width = 1;
    this.BlockKey = "V";

    this.Positions = [];
    for (let i = 0; i < this.Height; i++) {
      const x = this.Left;
      const y = this.Bottom + i;
      this.GetSetBlock(x, y, tower);
    }
  }
}