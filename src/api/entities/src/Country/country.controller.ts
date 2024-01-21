import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { CountryService } from './country.service';

@Controller('country')
export class CountryController {
    constructor(private readonly countryService: CountryService) {}


    @Post()
    async create(@Body() data: { name: string }) {
      return this.countryService.create(data);
    }
  
    @Get(':id')
    async findOne(@Param('id') id: string) {
      return this.countryService.getById(id);
    }

    @Get()
    async findAll() {
      return this.countryService.findAll();
    }

    @Put(':id')
    async update(@Param('id') id: string, @Body() data: { name: string }) {
      return this.countryService.update(id, data);
    }

    @Delete(':id')
    async delete(@Param('id') id: string) {
      await this.countryService.delete(id);
      return { message: `Country with id ${id} deleted successfully` };
    }
}
