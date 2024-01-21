import { Injectable, ConflictException, NotFoundException   } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class WineService {
  private prisma = new PrismaClient();

  async create(data: { name: string, points: number, price: string, variety: string, province_name: string, taster_name: string, winery_name: string}): Promise<any> {
    const { name, points, price, variety, province_name, taster_name, winery_name } = data;

    const province = await this.prisma.province.findFirst({
      where: { name: province_name },
    });

    if (!province) {
      throw new NotFoundException(`Province with name ${province_name} not found`);
    }

    const taster = await this.prisma.taster.findFirst({
      where: { name: taster_name },
    });

    if (!taster) {
      throw new NotFoundException(`Taster with name ${taster_name} not found`);
    }

    const winery = await this.prisma.winery.findFirst({
      where: { name: winery_name },
    });

    if (!winery) {
      throw new NotFoundException(`Winery with name ${winery_name} not found`);
    }

    return this.prisma.wine.create({
      data: {
        name,
        points,
        price: parseFloat(price),
        variety,
        province: { connect: { id: province.id } },
        taster: { connect: { id: taster.id } },
        winery: { connect: { id: winery.id } },
      },
    });
  }
  

  async getById(id: string): Promise<any | null> {
    const wine = await this.prisma.wine.findUnique({
      where: { id },
    });

    if (!wine) {
      throw new NotFoundException(`Wine with id ${id} not found`);
    }

    return wine;
  }

  async findAll(): Promise<any[]> {
    return this.prisma.wine.findMany();
  }
  
  async update(id: string, data: { name?: string, points?: number, price?: string, variety?: string }): Promise<any> {
    const existingWine = await this.prisma.wine.findUnique({
      where: { id },
    });
  
    if (!existingWine) {
      throw new NotFoundException(`Wine with id ${id} not found`);
    }
  
    // Convert price to number or leave it as is if undefined
    const updatedData: { name?: string, points?: number, price?: number, variety?: string } = {
      name: data.name,
      points: data.points,
      price: data.price ? parseFloat(data.price) : undefined,
      variety: data.variety,
    };
  
    return this.prisma.wine.update({
      where: { id },
      data: updatedData,
    });
  }
  

  async delete(id: string): Promise<void> {
    const existingWine = await this.prisma.wine.findUnique({
      where: { id },
    });

    if (!existingWine) {
      throw new NotFoundException(`Wine with id ${id} not found`);
    }

    await this.prisma.wine.delete({
      where: { id },
    });
  }
}
