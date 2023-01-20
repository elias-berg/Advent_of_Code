import { Block } from "./Block.js";
import Tower from "../Tower.js";

export class SquareBlock extends Block {
  constructor(tower: Tower) {
    super(tower);

    this.Height = 2;
    this.Width = 2;
    this.BlockKey = "S";

    this.Positions = [];
    // Hard-coded because I somehow couldn't write the double-nested loop right and
    // it's trivial to just code it like this anyway.
    let x = this.Left;
    let y = this.Bottom;
    this.GetSetBlock(x, y, tower); // Bottom-left
    x = this.Left + 1;
    y = this.Bottom;
    this.GetSetBlock(x, y, tower); // Bottom-right
    x = this.Left;
    y = this.Bottom + 1;
    this.GetSetBlock(x, y, tower); // Top-left
    x = this.Left + 1;
    y = this.Bottom + 1;
    this.GetSetBlock(x, y, tower); // Top-right
  }
}