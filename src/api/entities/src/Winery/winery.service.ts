import { Injectable, ConflictException, NotFoundException   } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class WineryService {
  private prisma = new PrismaClient();

  async create(data: { name: string }): Promise<any> {
    return this.prisma.winery.create({
      data: {
        name: data.name,
      },
    });
  }
  

  async getById(id: string): Promise<any | null> {
    const winery = await this.prisma.winery.findUnique({
      where: { id },
    });

    if (!winery) {
      throw new NotFoundException(`Winery with id ${id} not found`);
    }

    return winery;
  }

  async findAll(): Promise<any[]> {
    return this.prisma.winery.findMany();
  }

  async update(id: string, data: { name: string }): Promise<any> {
    const existingWinery = await this.prisma.winery.findUnique({
      where: { id },
    });

    if (!existingWinery) {
      throw new NotFoundException(`Winery with id ${id} not found`);
    }

    return this.prisma.winery.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    const existingWinery = await this.prisma.winery.findUnique({
      where: { id },
    });

    if (!existingWinery) {
      throw new NotFoundException(`Winery with id ${id} not found`);
    }

    await this.prisma.winery.delete({
      where: { id },
    });
  }
}
