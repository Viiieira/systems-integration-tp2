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
}
