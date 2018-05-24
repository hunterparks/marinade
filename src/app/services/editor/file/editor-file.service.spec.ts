import { TestBed, inject } from '@angular/core/testing';

import { EditorFileService } from './editor-file.service';

describe('EditorFileService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [EditorFileService]
    });
  });

  it('should be created', inject([EditorFileService], (service: EditorFileService) => {
    expect(service).toBeTruthy();
  }));
});
