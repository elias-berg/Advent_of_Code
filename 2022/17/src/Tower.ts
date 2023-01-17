
class Tower {
  public static readonly TOWER_WIDTH = 7;

  public TowerHeight: number; // The main thing we're looking for here

  private Root: JQuery<HTMLElement>;
  private TowerAry: JQuery<HTMLElement>[][];

  constructor(root: JQuery<HTMLElement>) {
    this.Root = root;
    if (!this.Root) {
      return;
    }

    this.TowerHeight = 0;

    // The tower is exactly 7 units wide
    // Each rock appears so that its left edge is 2 units away from the left wall and its bottom is 3 units above
    // the highest rock in the room (or floor when no rocks)
    this.TowerAry = [];
    for (let y = 0; y < 4; y++) { // 4 is the default starting height
      const rowElem = $("<tr/>");
      const towerRow = [];
      for (let x = 0; x < Tower.TOWER_WIDTH; x++) {
        const title = "x" + x + "y" + y;
        const cell = $("<td/>", { id: title, title, text: "-" }); // Instead of '.' we'll use a '-'

        rowElem.append(cell);
        towerRow.push(cell);
      }
      this.Root.prepend(rowElem);
      this.TowerAry.push(towerRow);
    }
  }

  /**
   * Simple wrapper around the tower container height.
   * @returns Total height of the tower's table container.
   */
  public Top(): number {
    return this.TowerAry.length; // 0-indexed array
  }

  /**
   * Wrapper around getting a specific element in the tower.
   * @param x X-coordinate to get.
   * @param y Y-coordinate to get.
   * @returns The jQuery element corresponding to the position.
   */
  public Get(x: number, y: number): JQuery<HTMLElement> {
    return this.TowerAry[y][x];
  }

  /**
   * Appends a row to the top of the tower container.
   */
  public AppendTopRow() {
    const y = this.TowerAry.length;

    // Create the jQuery elements
    const rowElem = $("<tr/>");
    const towerRow = [];
    for (let x = 0; x < Tower.TOWER_WIDTH; x++) {
      const title = "x" + x + "y" + y;
      const cell = $("<td/>", { id: title, title, text: "-" }); // Instead of '.' we'll use a '-'

      rowElem.append(cell);
      towerRow.push(cell);
    }
    this.Root.prepend(rowElem);
    this.TowerAry.push(towerRow);
  }
}

export default Tower;