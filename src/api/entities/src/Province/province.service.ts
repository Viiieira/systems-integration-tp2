import { Injectable, ConflictException, NotFoundException   } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class ProvinceService {
  private prisma = new PrismaClient();

  async create(data: { name: string, latitude: string, longitude: string, countryName: string}): Promise<any> {
    const { name, latitude, longitude, countryName } = data;

    const country = await this.prisma.country.findFirst({
      where: { name: countryName },
    });

    if (!country) {
      throw new NotFoundException(`Country with name ${countryName} not found`);
    }


    return this.prisma.province.create({
      data: {
        name: data.name,
        coords: { latitude: parseFloat(latitude), longitude: parseFloat(longitude) },
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
}
