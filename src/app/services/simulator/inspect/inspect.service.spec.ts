import { TestBed, inject } from '@angular/core/testing';

import { InspectService } from './inspect.service';

describe('InspectService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [InspectService]
    });
  });

  it('should be created', inject([InspectService], (service: InspectService) => {
    expect(service).toBeTruthy();
  }));
});
