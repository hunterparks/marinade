import { TestBed, inject } from '@angular/core/testing';

import { TransmitService } from './transmit.service';

describe('TransmitService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TransmitService]
    });
  });

  it('should be created', inject([TransmitService], (service: TransmitService) => {
    expect(service).toBeTruthy();
  }));
});
