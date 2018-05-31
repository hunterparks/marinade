import { TestBed, inject } from '@angular/core/testing';

import { BusMonitorService } from './bus-monitor.service';

describe('BusMonitorService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BusMonitorService]
    });
  });

  it('should be created', inject([BusMonitorService], (service: BusMonitorService) => {
    expect(service).toBeTruthy();
  }));
});
