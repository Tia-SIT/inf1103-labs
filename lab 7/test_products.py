from inventory_manager import PhysicalProduct, DigitalProduct

guitar = PhysicalProduct("P100", "Guitar", 450.0, 5, 3.2)
os_disc = DigitalProduct("D100", "Operating System", 99.0, 1000, 4500)

guitar.display_information()
os_disc.display_information()