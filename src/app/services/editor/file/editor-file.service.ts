import { Injectable } from '@angular/core';

@Injectable()
export class EditorFileService {

  private content: string;
  private dirty: boolean;
  private name: string;
  private path: string;

  constructor() { }

  public getContent(): string {
    return this.content;
  }

  public getDirtyFlag(): boolean {
    return this.dirty;
  }

  public getFileName(): string {
    return this.name;
  }

  public getFilePath(): string {
    return this.path;
  }

  public updateContent(newContent: string): void {
    if (newContent !== this.content) {
      this.dirty = true;
      this.content = newContent;
    }
  }

  public updateDirtyFlag(isDirty: boolean): void {
    this.dirty = isDirty;
  }

  public updateFilename(newName: string): void {
    this.name = newName;
  }

  public updateFilepath(newPath: string): void {
    this.path = newPath;
  }

}
