import { Test, TestingModule } from '@nestjs/testing';
import { WineController } from './wine.controller';

describe('WineController', () => {
  let controller: WineController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [WineController],
    }).compile();

    controller = module.get<WineController>(WineController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
