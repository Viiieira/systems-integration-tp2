import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { TasterService } from './taster.service';

@Controller('taster') // Corrected controller name to match the service
export class TasterController {
  constructor(private readonly tasterService: TasterService) {}

  @Post()
  async create(@Body() data: { name: string, twitter_handle: string }) {
    return this.tasterService.create(data);
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.tasterService.getById(id);
  }

  @Get()
  async findAll() {
    return this.tasterService.findAll();
  }
}
