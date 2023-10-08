from agent.scooter.scooter_controls import ScooterInterface


if __name__ == '__main__':
    print('Please Input Scooter Id: ', end='')
    scooter_id = int(input())

    scooter = ScooterInterface(scooter_id)
    scooter.scooter_startup()
