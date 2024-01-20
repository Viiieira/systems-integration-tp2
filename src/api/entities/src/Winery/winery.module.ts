import { Module } from '@nestjs/common';
import { WineryService } from './winery.service';
import { WineryController } from './winery.controller';

@Module({
  providers: [WineryService],
  controllers: [WineryController]
})
export class WineryModule {}
