import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { WineService } from './wine.service';

@Controller('wine')
export class WineController {
  constructor(private readonly wineService: WineService) {}

  @Post()
  async create(@Body() data: { name: string, points: number, price: number, variety: string, id_province: string, id_taster: string, id_winery: string }) {
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

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: { name?: string, points?: number, price?: number, variety?: string, id_province?: string, id_taster?: string, id_winery?: string }) {
    return this.wineService.update(id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string) {
    return this.wineService.delete(id);
  }
}
