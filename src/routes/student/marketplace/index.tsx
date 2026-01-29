import { createFileRoute } from '@tanstack/react-router'
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
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"

export const Route = createFileRoute('/student/marketplace/')({
  component: RouteComponent,
})

function RouteComponent() {
  const products = [
    {
      id: "p1",
      name: "School Hoodie",
      description: "Warm branded hoodie for students",
      price: 350,
      stock: 12,
      image: "https://picsum.photos/200?1",
      category: "Merch",
      featured: true,
    },
    {
      id: "p2",
      name: "Notebook Set",
      description: "3 premium notebooks",
      price: 120,
      stock: 25,
      image: "https://picsum.photos/200?2",
      category: "Stationery",
      featured: false,
    },
    {
      id: "p3",
      name: "Cafeteria Voucher",
      description: "Free meal coupon",
      price: 200,
      stock: 8,
      image: "https://picsum.photos/200?3",
      category: "Vouchers",
      featured: true,
    },
  ]

  return (
    <div className="min-h-screen bg-background p-1">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="max-w mx-auto space-y-3"
      >
        {/* Header */}
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
          <div className="flex gap-3 overflow-x-auto pb-2">
            <Carousel>
              <CarouselContent>
                {products
                  .filter((p) => p.featured)
                  .map((p) => (
                    <CarouselItem>
                      <motion.div key={p.id} whileHover={{ scale: 1.02 }}>
                        <Card className="shrink-0 rounded-2xl shadow-sm">
                          <CardContent className="p-3 space-y-2 w-full">
                            <img
                              src={p.image}
                              alt={p.name}
                              className="w-full aspect-square object-cover rounded-xl"
                            />
                            <div className="space-y-1">
                              <div className="flex items-center gap-1">
                                <Star className="h-3 w-3 text-yellow-500" />
                                <p className="text-sm font-medium leading-none">{p.name}</p>
                              </div>
                              <p className="text-xs text-muted-foreground line-clamp-2">
                                {p.description}
                              </p>
                            </div>
                            <div className="flex items-center justify-between">
                              <span className="flex items-center gap-1 font-semibold">
                                {p.price} <Coins className="h-4 w-4 text-primary" />
                              </span>
                              <Button size="sm" className="rounded-xl">Buy</Button>
                            </div>
                          </CardContent>
                        </Card>
                      </motion.div>
                    </CarouselItem>
                  ))}
              </CarouselContent>
              <CarouselPrevious />
              <CarouselNext />
            </Carousel>
          </div>
        </div>

        {/* All Products */}
        <div className="grid grid-cols-2 gap-3">
          {products.map((p) => (
            <motion.div key={p.id} whileHover={{ scale: 1.02 }}>
              <Card className="rounded-2xl shadow-sm">
                <CardContent className="p-3 space-y-2">
                  <img
                    src={p.image}
                    alt={p.name}
                    className="w-full aspect-square object-cover rounded-xl"
                  />
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">{p.name}</p>
                    <p className="text-xs text-muted-foreground line-clamp-2">
                      {p.description}
                    </p>
                  </div>
                  <div className="flex items-center justify-between">
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
                  {p.stock < 10 && (
                    <Badge variant="outline" className="text-xs w-fit">
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
