import { Test, TestingModule } from '@nestjs/testing';
import { WineryController } from './winery.controller';

describe('WineryController', () => {
  let controller: WineryController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [WineryController],
    }).compile();

    controller = module.get<WineryController>(WineryController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
