import { Module } from '@nestjs/common';
import { TasterService } from './taster.service';
import { TasterController } from './taster.controller';

@Module({
  providers: [TasterService],
  controllers: [TasterController]
})
export class TasterModule {}
