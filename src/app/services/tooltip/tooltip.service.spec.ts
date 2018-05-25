import { TestBed, inject } from '@angular/core/testing';

import { TooltipService } from '@services/tooltip/tooltip.service';

describe('TooltipService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TooltipService]
    });
  });

  it('should be created', inject([TooltipService], (service: TooltipService) => {
    expect(service).toBeTruthy();
  }));
});
