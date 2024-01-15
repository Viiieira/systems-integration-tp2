import { Injectable, ConflictException, NotFoundException } from '@nestjs/common';
import { PrismaClient, Wine } from '@prisma/client';

@Injectable()
export class WineService {
  private prisma = new PrismaClient();

  async create(data: { name: string, points: number, price: number, variety: string, id_province: string, id_taster: string, id_winery: string }): Promise<Wine> {
    const existingWine = await this.prisma.wine.findUnique({
      where: { name: data.name },
    });

    if (existingWine) {
      throw new ConflictException('Wine with the same name already exists');
    }

    return this.prisma.wine.create({
      data,
    });
  }

  async getById(id: string): Promise<Wine | null> {
    const wine = await this.prisma.wine.findUnique({
      where: { id },
    });

    if (!wine) {
      throw new NotFoundException(`Wine with id ${id} not found`);
    }

    return wine;
  }

  async findAll(): Promise<Wine[]> {
    return this.prisma.wine.findMany();
  }

  async update(id: string, data: { name?: string, points?: number, price?: number, variety?: string, id_province?: string, id_taster?: string, id_winery?: string }): Promise<Wine> {
    if (data.name) {
      const existingWine = await this.prisma.wine.findFirst({
        where: { name: data.name, id: { not: id } },
      });

      if (existingWine) {
        throw new ConflictException('Wine with the same name already exists');
      }
    }

    const updatedWine = await this.prisma.wine.update({
      where: { id },
      data,
    });

    return updatedWine;
  }

  async delete(id: string): Promise<Wine> {
    const deletedWine = await this.prisma.wine.delete({
      where: { id },
    });

    return deletedWine;
  }
}
