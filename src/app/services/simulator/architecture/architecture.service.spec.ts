import { TestBed, inject } from '@angular/core/testing';

import { ArchitectureService } from './architecture.service';

describe('ArchitectureService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ArchitectureService]
    });
  });

  it('should be created', inject([ArchitectureService], (service: ArchitectureService) => {
    expect(service).toBeTruthy();
  }));
});
