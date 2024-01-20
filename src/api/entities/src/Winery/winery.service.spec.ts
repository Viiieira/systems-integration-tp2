import { Test, TestingModule } from '@nestjs/testing';
import { WineryService } from './winery.service';

describe('WineryService', () => {
  let service: WineryService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [WineryService],
    }).compile();

    service = module.get<WineryService>(WineryService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
