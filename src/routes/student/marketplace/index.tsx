import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useState } from 'react'
import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Coins, Search, ShoppingCart, Star } from "lucide-react"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  type CarouselApi,
} from "@/components/ui/carousel"
import { type Product } from "@/types/product"

export const Route = createFileRoute('/student/marketplace/')({
  component: RouteComponent,
})

function RouteComponent() {
  const [featuredCarouselApi, setFeaturedCarouselApi] = useState<CarouselApi | null>(null)
  const [products, setProducts] = useState<Product[]>([])

  useEffect(() => {
    async function getProducts() {
      const response = await fetch('/api/products/list-active')
      if (!response.ok) {
        throw new Error('Failed to fetch products')
      }
      const data = await response.json() as Product[]
      setProducts(data)
    }
    void getProducts()
  }, [])

  useEffect(() => {
    if (!featuredCarouselApi) return
    const interval = setInterval(() => {
      featuredCarouselApi.scrollNext()
    }, 5000)
    return () => clearInterval(interval)
  }, [featuredCarouselApi])

  return (
    <div className="min-h-screen bg-background p-1">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="max-w mx-auto space-y-3"
      >
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4 space-y-3">
            <div className="flex items-center justify-between">
              <p className="font-semibold text-lg">Marketplace</p>
              <Button size="icon" variant="ghost" className="rounded-full">
                <ShoppingCart className="h-5 w-5" />
              </Button>
            </div>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Search products..." className="pl-9 rounded-xl" />
            </div>
          </CardContent>
        </Card>

        <div className="space-y-2">
          <p className="text-sm font-medium px-1">Featured</p>
          <div className="w-full pb-2">
            <Carousel
              className="w-full"
              opts={{ loop: true }}
              setApi={setFeaturedCarouselApi}
            >
              <CarouselContent className="ml-0">
                {products
                  .filter((p) => p.is_featured)
                  .map((p) => (
                    <CarouselItem key={p.id} className="pl-0 w-full basis-full">
                      <Card className="rounded-2xl shadow-sm w-full h-100 flex flex-col overflow-hidden">
                        <CardContent className="p-3 flex flex-col flex-1 min-h-0 w-full">
                          <img
                            src={p.image_url}
                            alt={p.name}
                            className="w-full h-64 object-cover rounded-xl shrink-0"
                          />
                          <div className="space-y-1 mt-2 flex-1 min-h-0">
                            <div className="flex items-center gap-1">
                              <Star className="h-3 w-3 text-yellow-500 shrink-0" />
                              <p className="text-sm font-medium leading-none truncate">{p.name}</p>
                            </div>
                            <p className="text-xs text-muted-foreground line-clamp-2">
                              {p.description}
                            </p>
                          </div>
                          <div className="flex items-center justify-between mt-2 shrink-0">
                            <span className="flex items-center gap-1 font-semibold">
                              {p.price} <Coins className="h-4 w-4 text-primary" />
                            </span>
                            <Button size="sm" className="rounded-xl">Buy</Button>
                          </div>
                        </CardContent>
                      </Card>
                    </CarouselItem>
                  ))}
              </CarouselContent>
            </Carousel>
          </div>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 items-stretch">
          {products.map((p) => (
            <motion.div key={p.id} whileHover={{ scale: 1.02 }} className="h-full min-h-0">
              <Card className="rounded-2xl shadow-sm h-full flex flex-col overflow-hidden">
                <CardContent className="p-3 flex flex-col flex-1 min-h-0">
                  <img
                    src={p.image_url}
                    alt={p.name}
                    className="w-full aspect-square object-cover rounded-xl shrink-0"
                  />
                  <div className="space-y-1 flex-1 min-h-0 mt-2">
                    <p className="text-sm font-medium leading-none">{p.name}</p>
                    <p className="text-xs text-muted-foreground line-clamp-2">
                      {p.description}
                    </p>
                  </div>
                  <div className="flex items-center justify-between mt-2 shrink-0">
                    <span className="flex items-center gap-1 font-semibold text-sm">
                      {p.price} <Coins className="h-4 w-4 text-primary" />
                    </span>
                    <Button
                      size="sm"
                      variant="secondary"
                      className="rounded-xl"
                    >
                      Buy
                    </Button>
                  </div>
                  {p.stock_quantity < 10 && p.is_active && (
                    <Badge variant="outline" className="text-xs w-fit mt-1 shrink-0">
                      Low stock
                    </Badge>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}
