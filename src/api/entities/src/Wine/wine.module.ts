import { Module } from '@nestjs/common';
import { WineService } from './wine.service';
import { WineController } from './wine.controller';

@Module({
  providers: [WineService],
  controllers: [WineController]
})
export class WineModule {}
