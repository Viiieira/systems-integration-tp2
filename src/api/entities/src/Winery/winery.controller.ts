import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { WineryService } from './winery.service';

@Controller('winery')
export class WineryController {
    constructor(private readonly wineryService: WineryService) {}


    @Post()
    async create(@Body() data: { name: string }) {
      return this.wineryService.create(data);
    }
  
    @Get(':id')
    async findOne(@Param('id') id: string) {
      return this.wineryService.getById(id);
    }

    @Get()
    async findAll() {
      return this.wineryService.findAll();
    }
}
