import { Input } from '@/components/ui/input'
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

interface ObjectiveInputProps {
    inputPlaceholder: string
    categoryPlaceholder: string
    sortPlaceholder: string
}

export default function ObjectiveInput({
    inputPlaceholder,
    categoryPlaceholder,
    sortPlaceholder
}: ObjectiveInputProps) {
    return (
        <div className='w-full flex flex-col gap-2 mb-4'>
            <div>
                <Input className='w-full' placeholder={inputPlaceholder}></Input>
            </div>
            <div className='w-full flex gap-2'>
                <Select>
                    <SelectTrigger className='w-full'>
                        <SelectValue placeholder={categoryPlaceholder} />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                            <SelectItem value="teacher">Teacher</SelectItem>
                            <SelectItem value="student">Student</SelectItem>
                        </SelectGroup>
                    </SelectContent>
                </Select>
                <Select>
                    <SelectTrigger className='w-full'>
                        <SelectValue placeholder={sortPlaceholder} />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                            { }
                        </SelectGroup>
                    </SelectContent>
                </Select>
            </div>
        </div>
    )
}