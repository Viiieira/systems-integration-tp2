import { Injectable, ConflictException, NotFoundException   } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class ProvinceService {
  private prisma = new PrismaClient();

  async create(data: { name: string, country_name: string}): Promise<any> {
    const { name, country_name } = data;

    const country = await this.prisma.country.findFirst({
      where: { name: country_name },
    });

    if (!country) {
      throw new NotFoundException(`Country with name ${country_name} not found`);
    }

    return this.prisma.province.create({
      data: {
        name: data.name,
        country: { connect: { id: country.id } },
      },
    });
  }
  

  async getById(id: string): Promise<any | null> {
    const province = await this.prisma.province.findUnique({
      where: { id },
    });

    if (!province) {
      throw new NotFoundException(`Province with id ${id} not found`);
    }

    return province;
  }

  async findAll(): Promise<any[]> {
    return this.prisma.province.findMany();
  }

  async update(id: string, data: { name: string, country_name: string }): Promise<any> {
    const { name, country_name } = data;

    const country = await this.prisma.country.findFirst({
      where: { name: country_name },
    });

    if (!country) {
      throw new NotFoundException(`Country with name ${country_name} not found`);
    }

    return this.prisma.province.update({
      where: { id },
      data: {
        name,
        country: { connect: { id: country.id } },
      },
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.province.delete({
      where: { id },
    });
  }
}
