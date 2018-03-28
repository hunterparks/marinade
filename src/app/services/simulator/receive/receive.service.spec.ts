import { TestBed, inject } from '@angular/core/testing';

import { ReceiveService } from './receive.service';

describe('ReceiveService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ReceiveService]
    });
  });

  it('should be created', inject([ReceiveService], (service: ReceiveService) => {
    expect(service).toBeTruthy();
  }));
});
