import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { WineService } from './wine.service';

@Controller('wine')
export class WineController {
    constructor(private readonly wineService: WineService) {}


    @Post()
    async create(@Body() data: { name: string, points: number, price: string, variety: string, province_name: string, taster_name: string, winery_name: string }) {
      return this.wineService.create(data);
    }
  
    @Get(':id')
    async findOne(@Param('id') id: string) {
      return this.wineService.getById(id);
    }

    @Get()
    async findAll() {
      return this.wineService.findAll();
    }
}
