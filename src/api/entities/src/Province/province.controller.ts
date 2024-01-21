import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { ProvinceService } from './province.service';

@Controller('province')
export class ProvinceController {
    constructor(private readonly provinceService: ProvinceService) {}


    @Post()
    async create(@Body() data: { name: string, country_name: string}) {
      return this.provinceService.create(data);
    }
  
    @Get(':id')
    async findOne(@Param('id') id: string) {
      return this.provinceService.getById(id);
    }

    @Get()
    async findAll() {
      return this.provinceService.findAll();
    }

    @Put(':id')
    async update(@Param('id') id: string, @Body() data: { name: string, country_name: string }) {
      return this.provinceService.update(id, data);
    }

    @Delete(':id')
    async delete(@Param('id') id: string) {
      await this.provinceService.delete(id);
      return { message: 'Province deleted successfully' };
    }
}
