import { Block } from "./Block.js";
import Tower from "../Tower.js";

export class HorizontalBlock extends Block {
  constructor(tower: Tower) {
    super(tower);

    this.Height = 1;
    this.Width = 4;

    this.Positions = [];
    for (let i = 0; i < this.Width; i++) {
      const x = this.Left + i;
      const y = this.Bottom;
      this.GetSetBlock(x, y, tower);
    }
  }
}