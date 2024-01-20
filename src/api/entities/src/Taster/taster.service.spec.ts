import { Test, TestingModule } from '@nestjs/testing';
import { TasterService } from './taster.service';

describe('TasterService', () => {
  let service: TasterService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [TasterService],
    }).compile();

    service = module.get<TasterService>(TasterService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
