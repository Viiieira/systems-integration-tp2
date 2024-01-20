import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CountryModule } from './Country/country.module';
import { TasterModule } from './Taster/taster.module';
import { ProvinceModule } from './Province/province.module';

@Module({
  imports: [CountryModule, ProvinceModule, TasterModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
