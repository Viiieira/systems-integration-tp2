import { Injectable, ConflictException, NotFoundException } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class TasterService {
  private prisma = new PrismaClient();

  async create(data: { name: string, twitter_handle: string }): Promise<any> {
    return this.prisma.taster.create({
      data: {
        name: data.name,
        twitter_handle: data.twitter_handle,
      },
    });
  }

  async getById(id: string): Promise<any | null> {
    const taster = await this.prisma.taster.findUnique({
      where: { id },
    });

    if (!taster) {
      throw new NotFoundException(`Taster with id ${id} not found`);
    }

    return taster;
  }

  async findAll(): Promise<any[]> {
    return this.prisma.taster.findMany();
  }

  async update(id: string, data: { name: string, twitter_handle: string }): Promise<any> {
    const existingTaster = await this.prisma.taster.findUnique({
      where: { id },
    });

    if (!existingTaster) {
      throw new NotFoundException(`Taster with id ${id} not found`);
    }

    return this.prisma.taster.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    const existingTaster = await this.prisma.taster.findUnique({
      where: { id },
    });

    if (!existingTaster) {
      throw new NotFoundException(`Taster with id ${id} not found`);
    }

    await this.prisma.taster.delete({
      where: { id },
    });
  }
}
