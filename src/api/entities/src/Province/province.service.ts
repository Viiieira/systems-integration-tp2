import { Injectable, ConflictException, NotFoundException } from '@nestjs/common';
import { PrismaClient, Province } from '@prisma/client';

@Injectable()
export class ProvinceService {
  private prisma = new PrismaClient();

  async create(data: { name: string, coords?: any }): Promise<Province> {
    // Check if a province with the same name already exists
    const existingProvince = await this.prisma.province.findUnique({
      where: { name: data.name },
    });
  
    if (existingProvince) {
      throw new ConflictException('Province with the same name already exists');
    }
  
    // Create a new province with optional coords
    return this.prisma.province.create({
      data: {
        name: data.name,
        coords: data.coords,
      },
    });
  }

  async getById(id: string): Promise<Province | null> {
    // Find a province by its ID
    const province = await this.prisma.province.findUnique({
      where: { id },
    });

    if (!province) {
      throw new NotFoundException(`Province with id ${id} not found`);
    }

    return province;
  }

  async findAll(): Promise<Province[]> {
    // Retrieve all provinces
    return this.prisma.province.findMany();
  }

  async update(id: string, data: { name?: string, coords?: any }): Promise<Province> {
    // Check if another province with the same name already exists
    if (data.name) {
      const existingProvince = await this.prisma.province.findFirst({
        where: { name: data.name, id: { not: id } },
      });
  
      if (existingProvince) {
        throw new ConflictException('Province with the same name already exists');
      }
    }
  
    // Update the province
    const updatedProvince = await this.prisma.province.update({
      where: { id },
      data: {
        name: data.name,
        coords: data.coords,
      },
    });
  
    return updatedProvince;
  }  

  async delete(id: string): Promise<Province> {
    const wines = await this.prisma.wine.findMany({
      where: { id_province: id },
    });

    if (wines.length > 0) {
      throw new ConflictException('Cannot delete province with existing wines');
    }

    const deletedProvince = await this.prisma.province.delete({
      where: { id },
    });

    return deletedProvince;
  }
}
