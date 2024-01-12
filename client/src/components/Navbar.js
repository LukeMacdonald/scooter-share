import React from 'react'

const CustomLink = ({href, title, className}) =>{
    return (
    <a href={href} className={`${className} relative group`}>
        {title}
    </a>
    )
}

const Navbar = () => {
  return (
    <header className='w-full px-32 py-8 font-medium flex items-center justify-between relative z-10 lg:px-16 md:px-12 sm:px-8'>
        <nav>
            <CustomLink href="/" title={"Home"} className='mr-4'/>
        </nav>

    </header>
  )
}

export default Navbar