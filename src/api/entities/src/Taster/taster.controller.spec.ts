import { Test, TestingModule } from '@nestjs/testing';
import { TasterController } from './taster.controller';

describe('TasterController', () => {
  let controller: TasterController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [TasterController],
    }).compile();

    controller = module.get<TasterController>(TasterController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
