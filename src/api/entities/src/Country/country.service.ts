import { Injectable, ConflictException, NotFoundException   } from '@nestjs/common';
import { PrismaClient, Country } from '@prisma/client';

@Injectable()
export class CountryService {
  private prisma = new PrismaClient();

  async create(data: { name: string }): Promise<Country> {
    const existingCountry = await this.prisma.country.findUnique({
      where: { name: data.name },
    });

    if (existingCountry) {
      throw new ConflictException('Country with the same name already exists');
    }

    return this.prisma.country.create({
      data,
    });
  }

  async getById(id: string): Promise<Country | null> {
    const country = await this.prisma.country.findUnique({
      where: { id },
    });

    if (!country) {
      throw new NotFoundException(`Country with id ${id} not found`);
    }

    return country;
  }

  async findAll(): Promise<any[]> {
    return this.prisma.country.findMany();
  }

  async update(id: string, data: { name: string }): Promise<Country> {
    const existingCountry = await this.prisma.country.findFirst({
      where: { name: data.name, id: { not: id } },
    });
  
    if (existingCountry) {
      throw new ConflictException('Country with the same name already exists');
    }
  
    const updatedCountry = await this.prisma.country.update({
      where: { id },
      data,
    });
  
    return updatedCountry;
  }    

  async delete(id: string): Promise<Country> {
    const provinces = await this.prisma.province.findMany({
      where: { id_country: id },
    });

    if (provinces.length > 0) {
      throw new ConflictException('Cannot delete country with existing provinces');
    }

    const deletedCountry = await this.prisma.country.delete({
      where: { id },
    });

    return deletedCountry;
  }
}
